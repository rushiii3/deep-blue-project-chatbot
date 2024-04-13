import React from "react";
import {
  FaReact,
  FaNodeJs,
  FaDatabase,
  FaPython,
  FaGoogle,
} from "react-icons/fa";
import { MdLanguage, MdLibraryBooks, MdExtension } from "react-icons/md";
import { BiLogoFlask } from "react-icons/bi";

const Technology = () => {
  const iconSizeClass = "w-8 h-8 text-deep-purple-accent-400 sm:w-10 sm:h-10";

  const techStack1 = [
    {
      heading: "React",
      shortInfo:
        "A JavaScript library for building user interfaces, particularly for single-page applications. It's known for its component-based architecture.",
      icon: <FaReact className={iconSizeClass} />,
    },
    {
      heading: "Express",
      shortInfo:
        "Express.js is a minimalist web application framework for Node.js, designed for building web applications and APIs.",
      icon: <FaNodeJs className={iconSizeClass} />,
    },
    {
      heading: "MongoDB",
      shortInfo:
        "A popular NoSQL database known for its flexibility and scalability, suitable for various applications, especially those handling high volumes of data.",
      icon: <FaDatabase className={iconSizeClass} />,
    },
    {
      heading: "NLTK (Natural Language Toolkit)",
      shortInfo:
        "A leading platform for building Python programs to work with human language data, providing easy-to-use interfaces and a suite of text processing libraries.",
      icon: <MdLanguage className={iconSizeClass} />,
    },
    {
      heading: "TensorFlow",
      shortInfo:
        "An open-source machine learning framework developed by Google, widely used for tasks such as image recognition, natural language processing, and numerical computations.",
      icon: <FaGoogle className={iconSizeClass} />,
    },
    {
        heading: "Flask",
        shortInfo:
          "A lightweight WSGI web application framework for Python, known for its simplicity and flexibility, suitable for building a wide range of web applications.",
        icon: <BiLogoFlask className={iconSizeClass} />,
      },
  ];

  const techStack2 = [
    {
      heading: "spaCy",
      shortInfo:
        "An open-source natural language processing library for Python, designed to be fast, efficient, and production-ready, offering pre-trained models and tools.",
      icon: <MdLibraryBooks className={iconSizeClass} />,
    },
    {
      heading: "PyMuPDF",
      shortInfo:
        "A Python binding for the MuPDF library, enabling manipulation of PDF documents programmatically, including tasks like text extraction and annotation.",
      icon: <MdExtension className={iconSizeClass} />,
    },
    {
      heading: "scikit-learn (or sklearn)",
      shortInfo:
        "A machine learning library for Python, providing simple and efficient tools for data mining and analysis, including classification, regression, and clustering.",
      icon: <FaPython className={iconSizeClass} />,
    },
    {
      heading: "PyTorch",
      shortInfo:
        "An open-source machine learning framework developed primarily by Facebook's AI Research lab, known for its dynamic computation graph suitable for deep learning.",
      icon: <FaPython className={iconSizeClass} />,
    },
    {
      heading: "Pandas",
      shortInfo:
        "A Python library for data manipulation and analysis, offering data structures and tools for various tasks including reading/writing data and data cleaning.",
      icon: <FaPython className={iconSizeClass} />,
    },
    {
      heading: "NumPy",
      shortInfo:
        "A fundamental package for scientific computing with Python, providing support for multi-dimensional arrays and a collection of mathematical functions.",
      icon: <FaPython className={iconSizeClass} />,
    },
    
  ];

  return (
    <div className="px-4 py-16 mx-auto sm:max-w-xl md:max-w-full lg:max-w-screen-xl md:px-24 lg:px-8 lg:py-20">
      <div className="max-w-xl mb-10 md:mx-auto sm:text-center lg:max-w-2xl md:mb-12">
        <div>
          {/* <p className="inline-block px-3 py-px mb-4 text-xs font-semibold tracking-wider text-teal-900 uppercase rounded-full bg-teal-accent-400">
            Brand new
          </p> */}
        </div>
        <h2 className="max-w-lg mb-6 font-sans text-3xl font-bold leading-none tracking-tight sm:text-4xl md:mx-auto uppercase text-indigo-500 dark:text-white">
          <span className="relative inline-block">
            <svg
              viewBox="0 0 52 24"
              fill="currentColor"
              className="absolute top-0 left-0 z-0 hidden w-32 -mt-8 -ml-20 text-blue-gray-100 lg:w-32 lg:-ml-28 lg:-mt-10 sm:block"
            >
              <defs>
                <pattern
                  id="07690130-d013-42bc-83f4-90de7ac68f76"
                  x="0"
                  y="0"
                  width=".135"
                  height=".30"
                >
                  <circle cx="1" cy="1" r=".7" />
                </pattern>
              </defs>
              <rect
                fill="url(#07690130-d013-42bc-83f4-90de7ac68f76)"
                width="52"
                height="24"
              />
            </svg>
            <span className="relative">Technologies</span>
          </span>{" "}
          used
        </h2>
        <p className="text-base text-gray-700 md:text-lg">
          Following are the technology are used to solve the problem
        </p>
      </div>
      <div className="grid max-w-screen-lg mx-auto space-y-6 lg:grid-cols-2 lg:space-y-0 lg:divide-x">
        <div className="space-y-6 sm:px-16">
          {techStack1.map((value, key) => (
            <div className="flex flex-col max-w-md sm:flex-row">
              <div className="mb-4 mr-4">
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-indigo-50">
                  {value.icon}
                </div>
              </div>
              <div>
                <h6 className="mb-3 text-xl font-bold leading-5">
                  {value.heading}
                </h6>
                <p className="text-sm text-gray-900 text-justify">
                  {value.shortInfo}
                </p>
              </div>
            </div>
          ))}
        </div>
        <div className="space-y-6 sm:px-16">
        {techStack2.map((value, key) => (
            <div className="flex flex-col max-w-md sm:flex-row">
              <div className="mb-4 mr-4">
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-indigo-50">
                  {value.icon}
                </div>
              </div>
              <div>
                <h6 className="mb-3 text-xl font-bold leading-5">
                  {value.heading}
                </h6>
                <p className="text-sm text-gray-900 text-justify">
                  {value.shortInfo}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Technology;
