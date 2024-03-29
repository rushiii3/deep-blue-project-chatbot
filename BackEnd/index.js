require("dotenv").config();
const express = require("express");
const multer = require("multer");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const bodyParser = require("body-parser");
const connectDB = require("./db");
const app = express();
const cloudinary = require("cloudinary").v2;
const fs = require("fs");
const File = require("./Models/FileModel");
const User = require("./Models/UserModel");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const { isAuthenticated } = require("./Middleware/auth");
const errorThrow = require("./Middleware/ErrorHandler");
cloudinary.config({
  cloud_name: "dmuhioahv",
  api_key: "166273865775784",
  api_secret: "blcMAs-77T_1t1VGnRIlLia_RqM",
  secure: true,
});

/* The `const storage` variable in the code snippet is creating a configuration object for Multer, a
middleware for handling file uploads in Node.js. */
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads/"); //location of pdf to save temporary
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname); //file saved
  },
});
const upload = multer({ storage: storage });

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true, limit: "50mb" }));
app.use(bodyParser.json());
app.use(
  cors({
    origin: "http://localhost:5173",
    credentials: true,
  })
);

// Connect to MongoDB
connectDB();
// create user
app.post("/register",async(req,res)=>{
  try {
    const {email,password} = req.body;
    const newUser = new User({
      firstname: 'John',
      lastname: 'Doe',
      email: 'admin@gmail.com',
      password: 'a12345678',
    });
    
    // Save the new user to the database
    newUser.save()
      .then(savedUser => {
        console.log('User saved successfully:', savedUser);
      })
      .catch(error => {
        console.error('Error saving user:', error);
      });
  } catch (error) {
    
  }
})
// login route
app.post("/login",async(req,res,next)=>{
  try {
    const {email,password} = req.body;
    if (!email || !password) {
      errorThrow("Email or password should not be empty", 400);
    }
    const userlogin = await User.findOne({ email }).select("+password");
    if (!userlogin) {
      errorThrow("User doesn't exist!", 404);
    }
    const isPasswordValid = await userlogin.comparePassword(password);
    if (!isPasswordValid) {
      errorThrow("Please provide the correct information", 401);
    }
    const UserToken = jwt.sign(
      JSON.stringify(userlogin),
      process.env.JWT_SECRET
    );
      
    const token = UserToken;
    const options = {
      expires: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000),
      httpOnly: false,
      sameSite: "none",
      secure: true,
    };
    const user = {
      firstname:userlogin.lastname,
      lastname:userlogin.firstname,
      _id:userlogin._id,
      email:userlogin.email
    }
    res.status(201).cookie("token", token, options).json({
      success: true,
      user,
      token,
    });
  } catch (error) {
    next(error)
  }
})

app.get("/getuser",isAuthenticated,async(req,res,next)=>{
  console.log(req.user);
  const userlogin =
    await User.findById(req.user).select(
      "email firstname  lastname _id "
    );
    console.log(userlogin);
    const user = {
      firstname:userlogin.firstname,
      lastname:userlogin.lastname,
      _id:userlogin._id,
      email:userlogin.email
    }
    res.status(200).json({ success: true, user: user });
})
// Route for file upload
app.post("/upload", upload.single("pdf"), async (req, res) => {
  try {
    const { filename, path } = req.file;
    if (!filename || !path) {
      errorThrow("Please input PDF", 500);
    }
    const result = await cloudinary.uploader.upload(path).catch((error) => {
      errorThrow(error.message, 500);
    });
    fs.unlink(path, (err) => {
      if (err) {
        console.error(err);
        return;
      }
      console.log("removed file");
    });
    if (!result) {
      errorThrow("Failed to upload pdf", 500);
    }
    const upload = await File.create({
      filename: filename,
      financial_year: "2023-2024",
      pdf: {
        public_id: result.public_id,
        url: result.secure_url,
      },
    });
    if (!upload) {
      errorThrow("Failed to upload pdf", 500);
    }
    res.json({ message: "File uploaded successfully" });
  } catch (error) {
    console.error("Error uploading file:", error);
    errorThrow("Error uploading file", 500);
  }
});

app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    message: err.message,
    stack: process.env.NODE_ENV === "development" ? err.stack : null,
    statuscode: statusCode,
  });
});

app.listen(process.env.PORT, () => {
  console.log(`Server is running on http://localhost:${process.env.PORT}`);
});

