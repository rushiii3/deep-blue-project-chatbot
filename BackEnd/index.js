require("dotenv").config();
const express = require('express');
const multer = require('multer');
const { GridFsStorage } = require('multer-gridfs-storage');
const Grid = require('gridfs-stream');
const cors = require('cors');
const connectDB = require('./db');
const mongoose = require('mongoose');

const app = express();


app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true,
}));

// Connect to MongoDB
connectDB();

// Set up GridFS
const conn = mongoose.connection;


// init gfs
let gfs;
conn.once('open', () => {
  gfs = Grid(conn.db, mongoose.mongo);
  gfs.collection('uploads');
  console.log('GridFS is ready');
});

// Storage
const storage = new GridFsStorage({
  url: process.env.MONGO_URl,
  file: (req, file) => {
    return {
      filename: file.originalname,
    };
  },
});

const upload = multer({ storage });


// Set up Multer and GridFS Storage




// Model for file information
const File = mongoose.model('File', {
  filename: String,
  fileId: mongoose.Types.ObjectId,
});

// Route for file upload
app.post('/upload', upload.single('pdf'), async (req, res) => {
  try {
    console.log('File uploaded successfully');
    const data = req.file;

    // Create a record in the File model with file information
    const newFile = new File({
      filename: data.originalname,
    });

    // Save the file information to MongoDB
    await newFile.save();

    console.log('File information saved to MongoDB');
    res.json({ message: 'File uploaded successfully' });
  } catch (error) {
    console.error('Error uploading file:', error);
    res.status(500).json({ error: 'Error uploading file' });
  }
});


// Route for downloading a file
// app.get('/download/:filename', (req, res) => {
//   try {
//     const { filename } = req.params;
//     console.log(gfs);
//     const fileinfo = gfs.files.findOne({ 
//       _id: mongoose.Types.ObjectId(req.params.filename)
//       // filename: req.params.filename.toString()
//     })
//     console.log(fileinfo);
//     // // Retrieve the file from GridFS
//     // const readstream = gfs.createReadStream({ filename });

//     // // Handle errors during streaming
//     // readstream.on('error', (err) => {
//     //   console.error('Error during file streaming:', err);
//     //   res.status(404).json({ error: 'File not found' });
//     // });

//     // // Stream the file to the response
//     // readstream.pipe(res);
//   } catch (error) {
//     console.error('Error during file download:', error);
//     res.status(500).json({ error: 'Error during file download' });
//   }
// });

app.get('/files', async (req, res) => {
  try {
    const files = await File.find();
    res.json(files);
  } catch (error) {
    console.error('Error fetching files:', error);
    res.status(500).json({ error: 'Error fetching files' });
  }
});

app.get('/files/:fileId', async (req, res) => {
  const { fileId } = req.params;
  console.log(fileId);
  try {
    const file = await File.findById(fileId);
    
    if (!file) {
      return res.status(404).json({ error: 'File not found' });
    }

    res.json(file);
  } catch (error) {
    console.error('Error fetching file details:', error);
    res.status(500).json({ error: 'Error fetching file details' });
  }
});

// Route for downloading a file by fileId
app.get('/download/:fileId', async (req, res) => {
  const { fileId } = req.params;

  try {
    const gfsFiles = conn.collection("fs.files");
    // console.log(gfsFiles);
    // const file2 = await gfsFiles.find();
    const file = await gfsFiles.findOne({ filename: fileId });
    if(!file) {
      res.status(400).json({success:false});
    }
    console.log(file);
    res.setHeader("Content-Disposition", `attachment; filename=${file.filename}`);
    res.setHeader("Content-Type", file.contentType);
    console.log("headers sent");
    gfs.createReadStream({ filename: file.filename }).pipe(res)
    console.log("sending response");
    // const file = await File.findById(fileId);

    // if (!file) {
    //   return res.status(404).json({ error: 'File not found' });
    // }
    // console.log(file.filename);
    // console.log(gfs.createReadStream);
    // // Retrieve the file from GridFS using its filename
    // const readstream = gfs.createReadStream({ filename: file.filename });

    // // Stream the file to the response
    // readstream.pipe(res);
  } catch (error) {
    console.error('Error downloading file:', error);
    res.status(500).json({ error: 'Error downloading file' });
  }
});

app.listen(process.env.PORT, () => {
  console.log(`Server is running on http://localhost:${process.env.PORT}`);
});
