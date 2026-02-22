const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const util = require('util');
const pipeline = util.promisify(require('stream').pipeline);

const fastify = require('fastify')({ logger: true });

fastify.register(require('@fastify/multipart'));

const UPLOAD_DIR = path.join(__dirname, '..', 'uploads');

// Ensure upload directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

fastify.post('/upload', async (req, reply) => {
  const data = await req.file();

  if (!data) {
    return reply.code(400).send({ error: 'No file uploaded' });
  }

  const filename = `${Date.now()}-${data.filename}`;
  const filepath = path.join(UPLOAD_DIR, filename);

  await pipeline(data.file, fs.createWriteStream(filepath));

  // Call Python AI Engine
  try {
    const pythonProcess = spawn('python3', ['ai_engine/main.py', filepath], {
      cwd: path.join(__dirname, '..') // Run from root to access ai_engine
    });

    let resultBuffer = '';
    let errorBuffer = '';

    for await (const chunk of pythonProcess.stdout) {
      resultBuffer += chunk;
    }

    for await (const chunk of pythonProcess.stderr) {
      errorBuffer += chunk;
    }

    const exitCode = await new Promise((resolve) => {
      pythonProcess.on('close', resolve);
    });

    if (exitCode !== 0) {
      req.log.error(`Python script failed with code ${exitCode}: ${errorBuffer}`);
      return reply.code(500).send({ error: 'AI Engine failed', details: errorBuffer });
    }

    try {
      const jsonResult = JSON.parse(resultBuffer);
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
    await fastify.listen({ port: 3000, host: '0.0.0.0' });
    console.log(`Server listening on ${fastify.server.address().port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
