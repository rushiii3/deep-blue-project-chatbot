import React, { useState } from 'react';
import ChatbotChatting from './ChatbotChatting';
const ChatDesign = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
      };
  return (
    <div className="fixed right-6 bottom-20 group z-50">
      
      <div
        id="speed-dial-menu-click"
        className={`flex flex-col items-center ${isMenuOpen ? 'block transition-all duration-500' : 'hidden'} mb-4 space-y-2`}
      >
       
        <ChatbotChatting />

      </div>


      {/* Menu Toggle Button */}
      <button
        type="button"
        data-dial-toggle="speed-dial-menu-click"
        data-dial-trigger="click"
        aria-controls="speed-dial-menu-click"
        aria-expanded={isMenuOpen}
        onClick={toggleMenu}
        name='ChatBotButton'
        class="fixed bottom-4 right-4 inline-flex items-center justify-center text-sm font-medium disabled:pointer-events-none disabled:opacity-50 border rounded-full w-16 h-16 bg-black hover:bg-gray-700 m-0 cursor-pointer border-gray-200 bg-none p-0 normal-case leading-5 hover:text-gray-900"      >
        {/* <img src="https://s3.ap-south-1.amazonaws.com/custpostimages/sb_images/loading.gif" alt=""  className='w-14 h-14'/> */}
        <svg xmlns=" http://www.w3.org/2000/svg" width="30" height="40" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
      class="text-white block border-gray-200 align-middle">
      <path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z" class="border-gray-200">
      </path>
    </svg>
      </button>
    </div>
  )
}

export default ChatDesign
