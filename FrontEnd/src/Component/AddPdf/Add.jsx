import React from "react";
import { useUserStore } from "../../Store/Store";
import TableView from "./TableView";

const Add = () => {
  const { isAuthenticated, user } = useUserStore();
  console.log(user);
  return (
    <div className="min-h-screen md:px-16 py-5 px-5">
      <h1 class="text-5xl my-5 font-bold leading-tight dark:text-white text-gray-800">
  Financial Reports
</h1>


      <TableView />
    </div>
  );
};

export default Add;
