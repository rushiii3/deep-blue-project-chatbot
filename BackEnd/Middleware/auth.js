const jwt = require("jsonwebtoken");
const asyncHandler = require("express-async-handler");
const errorThrow = require("./ErrorHandler");
const User = require("../Models/UserModel");
exports.isAuthenticated = asyncHandler(async(req,res,next) =>{
    const {token} = req.cookies;
    if(!token){
        return next(errorThrow("Please provide the correct information", 401));
    }
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded._id);
    next();
})