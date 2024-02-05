// file.model.js

const mongoose = require('mongoose');

const fileSchema = new mongoose.Schema({
  filename: {
    type: String,
    required: true,
  },
  fileId: {
    type: mongoose.Types.ObjectId,
    required: true,
  },
  uploadDate: {
    type: Date,
    default: Date.now,
  },
});

const File = mongoose.model('File', fileSchema);

module.exports = File;
