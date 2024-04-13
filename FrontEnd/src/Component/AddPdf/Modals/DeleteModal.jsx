import React from "react";
import {
  Modal,
  ModalContent,
  ModalBody,
  useDisclosure,
} from "@nextui-org/react";
import { MdDeleteOutline } from "react-icons/md";
import toast from "react-hot-toast";
import { link } from "../../../Links";
import axios from "axios";
import { useFinanceStore } from "../../../Store/Store";

const DeleteModal = ({ id }) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const { FinanceData, setFinanceData } = useFinanceStore();

  const deleteData = async (delete_id) => {
    const toastId = toast.loading("Deletingg...");
    try {
      const { data } = await axios.delete(`${link}/delete/${delete_id}`);
      if (data.success) {
        toast.success("Your report has been deleted", {
          id: toastId,
        });
        const updatedFinanceData = FinanceData.filter((item) => item._id !== delete_id);
        setFinanceData(updatedFinanceData);

      }
    } catch (error) {
      toast.error(error.message, {
        id: toastId,
      });
    } finally {
    }
  };
  return (
    <>
      <button type="button" onClick={onOpen}>
        <MdDeleteOutline />
      </button>

      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        classNames={{
          closeButton: "hidden",
        }}
        placement="center"
      >
        <ModalContent>
          {(onClose) => (
            <>
              <ModalBody className="p-0">
                <div class="relative transform overflow-hidden   text-left transition-all">
                  <div class=" px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                    <div class="sm:flex sm:items-start">
                      <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full  sm:mx-0 sm:h-10 sm:w-10">
                        <svg
                          class="h-6 w-6 text-red-600"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke-width="1.5"
                          stroke="currentColor"
                          aria-hidden="true"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
                          />
                        </svg>
                      </div>
                      <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                        <h3
                          class="text-base font-semibold leading-6 text-gray-900"
                          id="modal-title"
                        >
                          Delete Record
                        </h3>
                        <div class="mt-2">
                          <p class="text-sm text-gray-500">
                            Are you sure you want to delete report? This action
                            cannot be undone.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class=" px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                    <button
                      onClick={() => deleteData(id)}
                      type="button"
                      class="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:ml-3 sm:w-auto"
                    >
                      Delete
                    </button>
                    <button
                      onClick={onClose}
                      type="button"
                      class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </ModalBody>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

export default DeleteModal;
