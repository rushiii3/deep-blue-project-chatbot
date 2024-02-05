const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const { createReadStream } = require('stream');
const { GridFsStorage } = require('multer-gridfs-storage');
const Grid = require('gridfs-stream');

const app = express();
const PORT = 3000;

app.use(express.json());

// Connect to MongoDB
mongoose
  .connect('mongodb+srv://hrushiop:oq16yL7AoXMn1c3x@cluster0.h4boskd.mongodb.net/')
  .then(() => {
    console.log("Connected to MongoDB");
    app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
    });
  })
  .catch((error) => {
    console.error("MongoDB connection error:", error);
  });

// Set up GridFS
const conn = mongoose.connection;
let gfs;

conn.once('open', () => {
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection('uploads');
});

// Set up Multer and GridFS Storage
const storage = new GridFsStorage({
  url: 'mongodb://localhost:27017/your-database-name',
  file: (req, file) => {
    return {
      filename: file.originalname,
    };
  },
});

const upload = multer({ storage });

// Model for file information
const File = mongoose.model('File', {
  filename: String,
  fileId: mongoose.Types.ObjectId,
});

// Route for file upload
app.post('/upload', upload.single('pdf'), async (req, res) => {
  const { originalname } = req.file;

  // Create a record in the File model with file information
  const newFile = new File({
    filename: originalname,
  });

  // Save the file information to MongoDB
  try {
    await newFile.save();

    res.json({ message: 'File uploaded successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Error saving file information' });
  }
});

// Route for downloading a file
app.get('/download/:filename', (req, res) => {
  const { filename } = req.params;

  // Retrieve the file from GridFS
  const readstream = gfs.createReadStream({ filename });

  // Stream the file to the response
  readstream.pipe(res);
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
