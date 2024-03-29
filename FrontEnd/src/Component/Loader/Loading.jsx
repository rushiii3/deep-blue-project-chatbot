import React from "react";
import LoadingBar from 'react-top-loading-bar'

const Loading = () => {
  return (
    <div className="h-screen flex items-center justify-center">
      <div class="relative flex justify-center items-center">
        <div class="absolute animate-spin rounded-full h-32 w-32 border-t-4 border-b-4 border-purple-500"></div>
        <img
          src="https://www.svgrepo.com/show/509001/avatar-thinking-9.svg"
          class="rounded-full h-28 w-28"
        />
      </div>
    </div>
  );
};

export default Loading;
