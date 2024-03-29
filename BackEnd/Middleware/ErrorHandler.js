const errorThrow = (message,code) => {
    let error = new Error(message);
      error.statusCode = code;
      throw error
}
module.exports = errorThrow;