import React from "react";
import { Tooltip} from "@nextui-org/react";
import { MdOutlineRemoveRedEye } from "react-icons/md";
import { CiEdit } from "react-icons/ci";
import { MdDeleteOutline } from "react-icons/md";
const Actions = () => {
  return (
    <div className="relative flex items-center gap-2">
      <Tooltip content="Details">
        <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
            <MdOutlineRemoveRedEye />
        </span>
      </Tooltip>
      <Tooltip content="Edit">
        <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
          <CiEdit />
        </span>
      </Tooltip>
      <Tooltip color="danger" content="Delete">
        <span className="text-lg text-danger cursor-pointer active:opacity-50">
          <MdDeleteOutline />
        </span>
      </Tooltip>
    </div>
  );
};

export default Actions;
