import React, { useState } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
} from "@nextui-org/react";
import { IoMdAdd } from "react-icons/io";
import { useForm } from "react-hook-form";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import toast from "react-hot-toast";
import { link } from "../../../Links";
import axios from "axios";
import { useFinanceStore } from "../../../Store/Store";
const AddModal = () => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const {FinanceData, setFinanceData} = useFinanceStore();
  const schema = yup.object().shape({
    financialYear: yup
      .string()
      .required("Financial Year is required")
      .matches(
        /^\d{4}-\d{4}$/,
        "Invalid Financial Year format. Please use YYYY-YYYY format"
      ),
    pdf: yup
      .mixed()
      .required("A file is required")
      .test("fileRequired", "PDF File is required", (value) => {
        return value && value[0]?.type !== undefined;
      })
      .test("fileFormat", "PDF only", (value) => {
        console.log(value);
        return value && ["application/pdf"].includes(value[0]?.type);
      })
      .test("fileSize", "PDF size should be less than 10MB", (value) => {
        return value && value[0]?.size <= 10485760;
      }),
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm({
    resolver: yupResolver(schema),
    mode: "onTouched",
  });
  const pdfValue = watch("pdf");
  //   console.log("PDF Value:", pdfValue[0].name);
  const clearPdfField = () => {
    setValue("pdf", undefined); // Clear the value of the pdf field
  };

  const onSubmit = async (data) => {
    const toastId = toast.loading("Adding report...");
    try {
      const response = await axios.post(`${link}/upload`, data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      if (response.data.success) {
        reset();
        onOpenChange(!isOpen);
        toast.success("Your report has been added", {
          id: toastId,
        });
        setFinanceData([...FinanceData,response.data.upload]);
      }
    } catch (error) {
      toast.error(error.message, {
        id: toastId,
      });
    }
  };

  return (
    <>
      <Button
        onPress={onOpen}
        color="secondary"
        size="md"
        startContent={<IoMdAdd size={20} />}
      >
        Add
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                Add Financial Reports
              </ModalHeader>
              <ModalBody>
                <form
                  class="my-8 space-y-3"
                  onSubmit={handleSubmit(onSubmit)}
                  encType="multipart/form-data"
                >
                  <div class="grid grid-cols-1 space-y-2">
                    <label
                      className={`text-sm font-bold  tracking-wide ${
                        errors.financialYear ? "text-red-500" : "text-gray-500"
                      }`}
                    >
                      Financial Year
                    </label>
                    <input
                      className={`text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 ${
                        errors.financialYear ? "border-red-500" : ""
                      }`}
                      type="text"
                      placeholder="2023-2024"
                      {...register("financialYear")}
                    />
                    {errors.financialYear && (
                      <p className="text-red-500">
                        {errors.financialYear.message}
                      </p>
                    )}
                  </div>
                  <div class="grid grid-cols-1 space-y-2">
                    <label
                      class={`text-sm font-bold text-gray-500 tracking-wide ${
                        errors.pdf ? "text-red-500" : "text-gray-500"
                      } `}
                    >
                      Attach Document
                    </label>
                    <div class="flex items-center justify-center w-full">
                      <label
                        class={`flex flex-col rounded-lg border-4 border-dashed w-full h-60 p-10 group text-center ${
                          errors.pdf ? "border-red-400" : "border-gray-300"
                        } `}
                      >
                        <div class="h-full w-full text-center flex flex-col items-center justify-center  ">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="w-10 h-10 text-blue-400 group-hover:text-blue-600"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                            />
                          </svg>
                          <div class="flex flex-auto max-h-48 w-2/5 mx-auto -mt-10"></div>
                          <p class="pointer-none text-gray-500 ">
                            <span class="text-sm">Drag and drop</span> files
                            here <br /> or{" "}
                            <a
                              href=""
                              id=""
                              class="text-blue-600 hover:underline"
                            >
                              select a file
                            </a>{" "}
                            from your computer
                          </p>
                        </div>
                        <input
                          type="file"
                          className="hidden"
                          {...register("pdf")}
                        />
                      </label>
                    </div>
                  </div>
                  <p class="text-sm text-gray-300">
                    <span>File type: pdf only</span>
                  </p>
                  {errors.pdf && (
                    <p className="text-red-500">{errors.pdf.message}</p>
                  )}
                  {pdfValue && (
                    <div class="rounded-md bg-[#F5F7FB] py-4 px-8">
                      <div class="flex items-center justify-between">
                        <span class="truncate pr-3 text-base font-medium text-[#07074D]">
                          {pdfValue[0]?.name}
                        </span>
                        <button class="text-[#07074D]" onClick={clearPdfField}>
                          <svg
                            width="10"
                            height="10"
                            viewBox="0 0 10 10"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              fill-rule="evenodd"
                              clip-rule="evenodd"
                              d="M0.279337 0.279338C0.651787 -0.0931121 1.25565 -0.0931121 1.6281 0.279338L9.72066 8.3719C10.0931 8.74435 10.0931 9.34821 9.72066 9.72066C9.34821 10.0931 8.74435 10.0931 8.3719 9.72066L0.279337 1.6281C-0.0931125 1.25565 -0.0931125 0.651788 0.279337 0.279338Z"
                              fill="currentColor"
                            />
                            <path
                              fill-rule="evenodd"
                              clip-rule="evenodd"
                              d="M0.279337 9.72066C-0.0931125 9.34821 -0.0931125 8.74435 0.279337 8.3719L8.3719 0.279338C8.74435 -0.0931127 9.34821 -0.0931123 9.72066 0.279338C10.0931 0.651787 10.0931 1.25565 9.72066 1.6281L1.6281 9.72066C1.25565 10.0931 0.651787 10.0931 0.279337 9.72066Z"
                              fill="currentColor"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                  )}

                  <div>
                    <button
                      type="submit"
                      class="my-5 w-full flex justify-center bg-blue-500 text-gray-100 p-4  rounded-full tracking-wide
                                    font-semibold  focus:outline-none focus:shadow-outline hover:bg-blue-600 shadow-lg cursor-pointer transition ease-in duration-300"
                    >
                      Upload
                    </button>
                  </div>
                </form>
              </ModalBody>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

export default AddModal;
