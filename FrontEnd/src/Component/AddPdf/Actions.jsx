import React from "react";
import { Tooltip} from "@nextui-org/react";
import { CiEdit } from "react-icons/ci";
import ViewModal from "./Modals/ViewModal";
import DeleteModal from "./Modals/DeleteModal";
const Actions = ({data,setFinanceData, FinanceData}) => {
  return (
    <div className="relative flex items-center gap-2">
      <Tooltip content="Details">
        <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
            <ViewModal url={data?.pdf?.url} name={data?.filename.slice(0,-4)} setFinanceData={setFinanceData} FinanceData={FinanceData}/>
        </span>
      </Tooltip>
      <Tooltip content="Edit">
        <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
            
          <CiEdit />
        </span>
      </Tooltip>
      <Tooltip color="danger" content="Delete">
        <span className="text-lg text-danger cursor-pointer active:opacity-50">
            <DeleteModal id={data?._id} />
          
        </span>
      </Tooltip>
    </div>
  );
};

export default Actions;
