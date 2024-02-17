import React from "react";
import imgLogo from '../../assets/dcb3ee04e8748e585df1172d76cd7522 Background Removed.png'
import { Link } from "react-router-dom";
const Navbar = () => {
  return (
    <div>
      <header className="relative z-5 w-full h-24">
        <div className="container flex items-center justify-between h-full max-w-6xl px-8 mx-auto sm:justify-between xl:px-0">
          <a
            href="/"
            className="relative flex items-center h-5  font-black leading-none"
          >
            <img
              src={imgLogo}
              className="w-auto h-10 text-indigo-600 fill-current"
            />
            <span className="ml-2 text-xl text-gray-800">
              EcoDrive Motors<span className="text-pink-500">.</span>
            </span>
          </a>


          <div className="pb-8 mt-4 ml-auto   relative w-auto bg-transparent md:border-none md:mt-0 flex-row md:p-0 items-end flex justify-between">
            <Link to="/login"               className="relative z-40 px-3 py-2 mr-0 text-sm font-bold text-pink-500 md:px-5 lg:text-white sm:mr-3 md:mt-0"
>
Login
            </Link>
            
            <Link to="https://github.com/rushiii3/deep-blue-project-chatbot"               className="relative z-40 inline-block w-auto h-full px-5 py-3 text-sm font-bold leading-none text-white transition-all   duration-300 bg-indigo-700 rounded shadow-md fold-bold lg:bg-white lg:text-indigo-700 sm:w-full lg:shadow-none hover:shadow-xl"
>
            Get Code
            </Link>
           
            <svg
              className="absolute top-0 left-0 hidden w-screen max-w-3xl -mt-64 -ml-12 lg:block"
              viewBox="0 0 818 815"
              xmlns="http://www.w3.org/2000/svg"
              xmlnsXlink="http://www.w3.org/1999/xlink"
            >
              <defs>
                <linearGradient x1="0%" y1="0%" x2="100%" y2="100%" id="c">
                  <stop stopColor="#E614F2" offset="0%" />
                  <stop stopColor="#FC3832" offset="100%" />
                </linearGradient>
                <linearGradient x1="0%" y1="0%" x2="100%" y2="100%" id="f">
                  <stop stopColor="#657DE9" offset="0%" />
                  <stop stopColor="#1C0FD7" offset="100%" />
                </linearGradient>
                <filter
                  x="-4.7%"
                  y="-3.3%"
                  width="109.3%"
                  height="109.3%"
                  filterUnits="objectBoundingBox"
                  id="a"
                >
                  <feOffset
                    dy={8}
                    in="SourceAlpha"
                    result="shadowOffsetOuter1"
                  />
                  <feGaussianBlur
                    stdDeviation={8}
                    in="shadowOffsetOuter1"
                    result="shadowBlurOuter1"
                  />
                  <feColorMatrix
                    values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.15 0"
                    in="shadowBlurOuter1"
                  />
                </filter>
                <filter
                  x="-4.7%"
                  y="-3.3%"
                  width="109.3%"
                  height="109.3%"
                  filterUnits="objectBoundingBox"
                  id="d"
                >
                  <feOffset
                    dy={8}
                    in="SourceAlpha"
                    result="shadowOffsetOuter1"
                  />
                  <feGaussianBlur
                    stdDeviation={8}
                    in="shadowOffsetOuter1"
                    result="shadowBlurOuter1"
                  />
                  <feColorMatrix
                    values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.2 0"
                    in="shadowBlurOuter1"
                  />
                </filter>
                <path
                  d="M160.52 108.243h497.445c17.83 0 24.296 1.856 30.814 5.342 6.519 3.486 11.635 8.602 15.12 15.12 3.487 6.52 5.344 12.985 5.344 30.815v497.445c0 17.83-1.857 24.296-5.343 30.814-3.486 6.519-8.602 11.635-15.12 15.12-6.52 3.487-12.985 5.344-30.815 5.344H160.52c-17.83 0-24.296-1.857-30.814-5.343-6.519-3.486-11.635-8.602-15.12-15.12-3.487-6.52-5.343-12.985-5.343-30.815V159.52c0-17.83 1.856-24.296 5.342-30.814 3.486-6.519 8.602-11.635 15.12-15.12 6.52-3.487 12.985-5.343 30.815-5.343z"
                  id="b"
                />
                <path
                  d="M159.107 107.829H656.55c17.83 0 24.296 1.856 30.815 5.342 6.518 3.487 11.634 8.602 15.12 15.12 3.486 6.52 5.343 12.985 5.343 30.816V656.55c0 17.83-1.857 24.296-5.343 30.815-3.486 6.518-8.602 11.634-15.12 15.12-6.519 3.486-12.985 5.343-30.815 5.343H159.107c-17.83 0-24.297-1.857-30.815-5.343-6.519-3.486-11.634-8.602-15.12-15.12-3.487-6.519-5.343-12.985-5.343-30.815V159.107c0-17.83 1.856-24.297 5.342-30.815 3.487-6.519 8.602-11.634 15.12-15.12 6.52-3.487 12.985-5.343 30.816-5.343z"
                  id="e"
                />
              </defs>
              <g fill="none" fillRule="evenodd" opacity={0.9}>
                <g transform="rotate(65 416.452 409.167)">
                  <use fill="#000" filter="url(#a)" xlinkHref="#b" />
                  <use fill="url(#c)" xlinkHref="#b" />
                </g>
                <g transform="rotate(29 421.929 414.496)">
                  <use fill="#000" filter="url(#d)" xlinkHref="#e" />
                  <use fill="url(#f)" xlinkHref="#e" />
                </g>
              </g>
            </svg>
          </div>

          {/* <div
            id="nav-mobile-btn"
            className="absolute top-0 right-0 z-50 block w-6 mt-8 mr-10 cursor-pointer select-none md:hidden sm:mt-10"
          >
            <span className="block w-full h-1 mt-2 duration-200 transform bg-gray-800 rounded-full sm:mt-1"></span>
            <span className="block w-full h-1 mt-1 duration-200 transform bg-gray-800 rounded-full"></span>
          </div> */}
        </div>
      </header>
    </div>
  );
};

export default Navbar;
