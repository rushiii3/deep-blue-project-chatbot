import React from "react";
import { useUserStore } from "../../Store/Store";
import TableView from "./TableView";
import AddModal from "./Modals/AddModal";

const Add = () => {
  const { isAuthenticated, user } = useUserStore();
  console.log(user);
  
  return (
    <div className="min-h-screen md:px-16 py-5 px-5">
      <div className="flex justify-between items-center">
        <h1 class="lg:text-5xl md:text-3xl text-xl my-5 font-bold leading-tight dark:text-white text-gray-800">
          Financial Reports
        </h1>
            <AddModal />
      </div>

      <TableView />
    </div>
  );
};

export default Add;
