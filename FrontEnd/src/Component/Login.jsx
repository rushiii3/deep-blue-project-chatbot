import React from "react";

const Login = () => {
  return (
    <>
     
     <div className="lg:flex">
            <div className="lg:w-1/2 xl:max-w-screen-sm">
                
                <div className="sm:px-24 md:px-12 px-12 mt-20 xl:px-24 xl:max-w-2xl p-6 sm:p-12">
                    <h2 className="text-center text-4xl text-indigo-900 font-display font-semibold lg:text-left xl:text-5xl
                    xl:text-bold">Log in</h2>
                    <div className="mt-12">
                        <form>
                            <div>
                                <div className="text-sm font-bold text-gray-700 tracking-wide">Email Address</div>
                                <input className="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500" type="" placeholder="mike@gmail.com" />
                            </div>
                            <div className="mt-8">
                                <div className="flex justify-between items-center">
                                    <div className="text-sm font-bold text-gray-700 tracking-wide">
                                        Password
                                    </div>
                                    <div>
                                        <a className="text-xs font-display font-semibold text-indigo-600 hover:text-indigo-800
                                        cursor-pointer">
                                            Forgot Password?
                                        </a>
                                    </div>
                                </div>
                                <input className="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500" type="" placeholder="Enter your password" />
                            </div>
                            <div className="mt-10">
                                <button className="bg-indigo-500 text-gray-100 p-4 w-full rounded-full tracking-wide
                                font-semibold font-display focus:outline-none focus:shadow-outline hover:bg-indigo-600
                                shadow-lg">
                                    Log In
                                </button>
                            </div>
                        </form>
                        <div className="mt-12 text-sm font-display font-semibold text-gray-700 text-center">
                            Don't have an account ? <a className="cursor-pointer text-indigo-600 hover:text-indigo-800">Sign up</a>
                        </div>
                    </div>
                </div>
            </div>
            <div className="hidden lg:flex items-center justify-center bg-indigo-100 flex-1 h-screen" style={{ 
      backgroundImage: `url("https://www.springboard.com/blog/wp-content/uploads/2020/12/Ai-general-4-scaled.jpg")` , backgroundRepeat:"no-repeat" , backgroundSize:"cover"
    }}>
                
            </div>
        </div>
    </>
  );
};

export default Login;
