import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
const ChatbotChatting = () => {
  const [Chat, setChat] = useState([
    // {
    //   message:
    //     "Hello there! Welcome to our chat service. My name is Chatbot and I'm here to assist you with any questions or concerns you may have. Whether you need help with product information, assistance with your account, or anything else, feel free to ask. I'm here to help! <p>Heyyy</p>",
    //   type: "b",
    // },
  ]);
  const [input, setinput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  };
  const handleSendMessage = async (msg) => {
    const inputData = input || msg;
    if (inputData) {
      const data = {
        message: inputData,
        type: "u",
      };
      setChat((prevChat) => [...prevChat, data]);
      setinput("");

      // Scroll to bottom after adding a new message
      scrollToBottom();

      const response = await axios.post(
        "https://chatbot-p7kt.onrender.com/predict",
        { message: inputData }
      );
      if (response.data.answer) {
        const data = {
          message: response.data.answer,
          type: "b",
        };
        setChat((prevChat) => [...prevChat, data]);
      }
    }
  };
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage(input);
    }
  };

  const onButtonClick = (msg) => {
    setinput(msg);
    handleSendMessage(msg);
  };
  useEffect(() => {
    // Scroll to bottom when Chat updates
    scrollToBottom();
  }, [Chat]);
  const buttonLabels = ["Describe the key metrics related to april.", "Analyze the trends in july.", "Describe the key metrics related to collaboration with siemens."];

  return (
    <div class="fixed bottom-[calc(4rem+1.5rem)] right-0 mr-4  bg-white p-6 rounded-lg border border-[#e5e7eb] w-md min-w-md max-w-md  h-[calc(100%-10rem)] dark:bg-black ">
      <div class="flex flex-col space-y-1.5 pb-6">
        <h2 class="font-semibold text-lg tracking-tight dark:text-white">
          Chatbot
        </h2>
        <p class="text-sm text-[#6b7280] leading-3 dark:text-white">
          Powered by
        </p>
      </div>

      <div class="pr-4 h-[calc(100%-7rem)]   overflow-y-scroll no-scrollbar ">
        <div class="flex gap-3 my-4 text-gray-600 text-sm flex-1">
          <span
            class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8"
            ref={messagesEndRef}
          >
            <div class="rounded-full bg-gray-100 border p-1">
              <svg
                stroke="none"
                fill="black"
                stroke-width="1.5"
                viewBox="0 0 24 24"
                aria-hidden="true"
                height="20"
                width="20"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                ></path>
              </svg>
            </div>
          </span>
          <p class="leading-relaxed text-justify dark:text-white">
            <span class="block font-bold text-gray-700 dark:text-white">
              AI
            </span>
            Hello there! Welcome to our financial report service. My name is
            Finbot and I'm here to assist you with any questions or concerns you
            may have. Whether you need help with financial data analysis,
            assistance with understanding your reports, or anything else related
            to financial information, feel free to ask. I'm here to help!
            <div class="max-w-full flex flex-col rounded-lg shadow-sm mt-3">
              {buttonLabels.map((label, index) => (
                <button
                  key={index}
                  type="button"
                  className={`py-3 px-4 inline-flex items-center gap-x-2 text-sm font-medium focus:z-10 border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-white dark:hover:bg-gray-800 ${
                    index === 0 ? "rounded-t-md" : ""
                  } ${
                    index !== 0 && index !== buttonLabels.length - 1
                      ? "-mt-px"
                      : ""
                  } ${
                    index === buttonLabels.length - 1
                      ? "rounded-b-md -mt-px"
                      : ""
                  }`}
                  onClick={() => {
                    onButtonClick(label);
                  }}
                >
                  {label}
                </button>
              ))}
            </div>
          </p>
        </div>

        <AnimatePresence initial={true}>
          {Chat?.map((value, key) => (
            <motion.div
              class="flex gap-3 my-4 text-gray-600 text-sm flex-1"
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, transition: { duration: 0.3 } }}
              key={key}
            >
              <span
                class="relative flex shrink-0 overflow-hidden rounded-full w-8 h-8"
                ref={messagesEndRef}
              >
                <div class="rounded-full bg-gray-100 border p-1">
                  {value?.type === "b" ? (
                    <svg
                      stroke="none"
                      fill="black"
                      stroke-width="1.5"
                      viewBox="0 0 24 24"
                      aria-hidden="true"
                      height="20"
                      width="20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                      ></path>
                    </svg>
                  ) : (
                    <svg
                      stroke="none"
                      fill="black"
                      stroke-width="0"
                      viewBox="0 0 16 16"
                      height="20"
                      width="20"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"></path>
                    </svg>
                  )}
                </div>
              </span>
              <p class="leading-relaxed text-justify dark:text-white">
                <span class="block font-bold text-gray-700 dark:text-white">
                  {" "}
                  {value?.type === "b" ? "AI" : "You"}{" "}
                </span>
                {value?.message}
              </p>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div class="flex items-center pt-2">
        <form class="flex items-center justify-center w-full space-x-2">
          <input
            class="flex h-10 w-full rounded-md border border-[#e5e7eb] px-3 py-2 text-sm placeholder-[#6b7280] focus:outline-none focus:ring-2 focus:ring-[#9ca3af] disabled:cursor-not-allowed disabled:opacity-50 text-[#030712] focus-visible:ring-offset-2"
            placeholder="Type your message"
            value={input}
            onInput={(e) => setinput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            type="button"
            onClick={() => {
              handleSendMessage("");
            }}
            class="inline-flex items-center justify-center rounded-md text-sm font-medium text-[#f9fafb] disabled:pointer-events-none disabled:opacity-50 bg-black hover:bg-[#111827E6] h-10 px-4 py-2 dark:border-white dark:border-1"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatbotChatting;
