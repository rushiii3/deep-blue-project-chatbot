import React, { useState } from "react";
import { useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { Input, Button } from "@nextui-org/react";
import { BsEye } from "react-icons/bs";
import { BsEyeSlash } from "react-icons/bs";
import {useUserStore} from "../Store/Store";
import axios from "axios";
import { link } from "../Links";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { setUser } = useUserStore();
  const navigator  = useNavigate();
  const [isVisible, setIsVisible] = useState(false);
  const toggleVisibility = () => setIsVisible(!isVisible);
  const schema = yup.object().shape({
    email: yup
      .string()
      .email("Invalid Email")
      .required("Please provide an email"),
    password: yup
      .string()
      .min(8, "Password must be greater than 8")
      .max(32, "Password must be less than 32")
      .required("Please provide a password"),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    resolver: yupResolver(schema),
  });
  const onSubmit = async (data) => {
    const toastId = toast.loading("Login...");

    try {
      const response = await axios.post(`${link}/login`, data,{withCredentials:true});
      if (response.data.success) {
        setUser(response.data.user);
        toast.success("Logged in successfully", {
          id: toastId,
        });
        reset();
        navigator('/add');
      }
    } catch (error) {
      toast.error(error.response.data.message, {
        id: toastId,
      });
    }
  };
  return (
    <>
      <div className="lg:flex flex justify-center min-h-screen">
        <div className="lg:w-1/2 xl:max-w-screen-sm">
          <div className="sm:px-24 md:px-12 px-12 mt-20 xl:px-24 xl:max-w-2xl p-6 sm:p-12">
            <h2 className="text-center text-4xl font-display font-semibold lg:text-left xl:text-5xl xl:text-bold text-indigo-900 dark:text-white">
              Log in
            </h2>
            <div className="mt-12 w-full">
              <form onSubmit={handleSubmit(onSubmit)}>
                <Input
                  size="lg"
                  type="email"
                  variant="underlined"
                  label="Email"
                  placeholder="Enter your email"
                  {...register("email")}
                  validationState={errors.email?.message ? "invalid" : "valid"}
                  errorMessage={errors.email?.message}
                />

                <Input
                  size="lg"
                  label="Password"
                  variant="underlined"
                  placeholder="Enter your password"
                  endContent={
                    <button
                      className="focus:outline-none"
                      type="button"
                      onClick={toggleVisibility}
                    >
                      {isVisible ? (
                        <BsEyeSlash className="text-2xl text-default-400 pointer-events-none" />
                      ) : (
                        <BsEye className="text-2xl text-default-400 pointer-events-none" />
                      )}
                    </button>
                  }
                  type={isVisible ? "text" : "password"}
                  className="max-w-full mt-3"
                  {...register("password")}
                  validationState={
                    errors.password?.message ? "invalid" : "valid"
                  }
                  errorMessage={errors.password?.message}
                />
                <div className="mt-10">
                  <button className="bg-indigo-500 text-gray-100 p-4 w-full rounded-full tracking-wide font-semibold font-display focus:outline-none focus:shadow-outline hover:bg-indigo-600 shadow-lg dark:bg-gray-800 dark:hover:bg-indigo-600 dark:text-gray-100">
                    Log In
                  </button>
                </div>
              </form>

              <div className="mt-12 text-sm font-display font-semibold text-gray-700 text-center dark:text-gray-300">
                Don't have an account?{" "}
                <a className="cursor-pointer text-indigo-600 hover:text-indigo-800">
                  Sign up
                </a>
              </div>
            </div>
          </div>
        </div>
        <div
          className="hidden lg:flex items-center justify-center bg-indigo-100 flex-1 h-screen"
          style={{
            backgroundImage: `url("https://www.springboard.com/blog/wp-content/uploads/2020/12/Ai-general-4-scaled.jpg")`,
            backgroundRepeat: "no-repeat",
            backgroundSize: "cover",
          }}
        ></div>
      </div>
    </>
  );
};

export default Login;
