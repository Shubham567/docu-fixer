const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const util = require('util');
const pipeline = util.promisify(require('stream').pipeline);
require('dotenv').config();

const fastify = require('fastify')({
  logger: {
    transport: {
      target: 'pino-pretty'
    }
  }
});

fastify.register(require('@fastify/multipart'), {
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB limit
    }
});

const UPLOAD_DIR = process.env.UPLOAD_DIR || path.join(__dirname, '..', 'uploads');

// Ensure upload directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

fastify.post('/upload', async (req, reply) => {
  const data = await req.file();

  if (!data) {
    return reply.code(400).send({ error: 'No file uploaded' });
  }

  // Validate MIME type
  if (data.mimetype !== 'application/pdf') {
      return reply.code(400).send({ error: 'Only PDF files are allowed' });
  }

  const filename = `${Date.now()}-${data.filename}`;
  const filepath = path.join(UPLOAD_DIR, filename);

  try {
    await pipeline(data.file, fs.createWriteStream(filepath));
  } catch (e) {
      req.log.error(`File write failed: ${e.message}`);
      return reply.code(500).send({ error: 'File upload failed' });
  }

  req.log.info(`File uploaded: ${filepath}`);

  // Call Python AI Engine
  // Using -m module execution to handle imports correctly
  try {
    const pythonProcess = spawn('python3', ['-m', 'ai_engine.main', filepath], {
      cwd: path.join(__dirname, '..'), // Run from root
      env: { ...process.env, PYTHONPATH: path.join(__dirname, '..') }
    });

    let resultBuffer = '';
    let errorBuffer = '';

    for await (const chunk of pythonProcess.stdout) {
      resultBuffer += chunk;
    }

    for await (const chunk of pythonProcess.stderr) {
      // Python logging goes to stderr, so we log it as info/debug unless process fails
      errorBuffer += chunk;
      process.stderr.write(chunk); // Stream logs to console
    }

    const exitCode = await new Promise((resolve) => {
      pythonProcess.on('close', resolve);
    });

    if (exitCode !== 0) {
      req.log.error(`Python script failed with code ${exitCode}`);
      return reply.code(500).send({ error: 'AI Engine failed', details: 'Check server logs for details.' });
    }

    try {
      // Find the JSON part in the output (in case there are other logs on stdout)
      // Assuming the last line is the JSON
      const lines = resultBuffer.trim().split('\n');
      const jsonLine = lines[lines.length - 1];
      const jsonResult = JSON.parse(jsonLine);
      return reply.send(jsonResult);
    } catch (e) {
      req.log.error(`Failed to parse JSON: ${resultBuffer}`);
      return reply.code(500).send({ error: 'Invalid response from AI Engine', raw: resultBuffer });
    }

  } catch (err) {
    req.log.error(err);
    return reply.code(500).send({ error: 'Internal Server Error' });
  } finally {
      // Clean up file after processing
      try {
        if (fs.existsSync(filepath)) {
          fs.unlinkSync(filepath);
        }
      } catch (e) {
        req.log.error(`Failed to delete file ${filepath}: ${e.message}`);
      }
  }
});

const start = async () => {
  try {
    const port = process.env.PORT || 3000;
    await fastify.listen({ port, host: '0.0.0.0' });
    console.log(`Server listening on ${port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
