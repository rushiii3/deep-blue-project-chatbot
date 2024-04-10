require("dotenv").config();
const production = true;
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
const { default: mongoose } = require("mongoose");

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
    origin: `${
      !production
        ? "http://localhost:5173"
        : "https://deep-blue-project-chatbot.vercel.app"
    }`,
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
// get user
app.get("/getuser",isAuthenticated,async(req,res,next)=>{
  const userlogin =
    await User.findById(req.user).select(
      "email firstname  lastname _id "
    );
    const user = {
      firstname:userlogin.firstname,
      lastname:userlogin.lastname,
      _id:userlogin._id,
      email:userlogin.email
    }
    res.status(200).json({ success: true, user: user });
})
// get finance records
app.get("/get-data",async(req,res,next)=>{
  try {
    const data = await File.find({});
    if (!data) {
      errorThrow("No data found", 400);
    }
    res.status(200).json({ success: true, data: data });
  } catch (error) {
    next(error)
  }
})
// Route for file upload
app.post("/upload", upload.single("pdf[]"), async (req, res) => {
  try {
    const {financialYear} = req.body;
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
      financial_year: financialYear,
      pdf: {
        public_id: result.public_id,
        url: result.secure_url,
      },
      isSelected:false
    });
    if (!upload) {
      errorThrow("Failed to upload pdf", 500);
    }
    res.json({success:true, message: "File uploaded successfully" , upload });
  } catch (error) {
    next(error)
  }
});
app.delete("/delete/:id",async(req,res,next)=>{
  try {
    const {id} = req.params;
    if(!mongoose.isValidObjectId(id)){
      errorThrow("Please enter a valid id", 400);
    }
    const file = await File.findById(id);
    await cloudinary.uploader
      .destroy(file.pdf.public_id)
      .then((result) => console.log(result));

    const deleteData = await File.findByIdAndDelete(id);
    if(!deleteData){
      errorThrow("Failed to delete the record", 400);
    }

    res.status(200).json({ success: true });
  } catch (error) {
    next(error);
  }
})

app.listen(process.env.PORT, () => {
  console.log(`Server is running on http://localhost:${process.env.PORT}`);
});

