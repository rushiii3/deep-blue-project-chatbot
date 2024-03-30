import React, { useEffect, useState } from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Spinner,
} from "@nextui-org/react";
import Actions from "./Actions";
import axios from "axios";
import { link } from "../../Links";
import { useFinanceStore, useLoader } from "../../Store/Store";

const TableView = () => {
  const { loading, setLoading } = useLoader();
    const {FinanceData, setFinanceData} = useFinanceStore();
  useEffect(() => {
    const getData = async () => {
      setLoading(true);
      try {
        // Simulate a delay of 2 seconds before making the API call
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const { data } = await axios.get(`${link}/get-data`);
        if (data.success) {
          setFinanceData(data.data);
          console.log(data.data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        // Ensure setLoading is always set to false after the API call, even if an error occurs
        setLoading(false);
      }
    };

    getData();
  }, []);

  return (
    <Table
      aria-label="Example static collection table"
      classNames={{
        wrapper: "max-h-[382px]",
      }}
    >
      <TableHeader>
        <TableColumn>NAME</TableColumn>
        <TableColumn>YEAR</TableColumn>
        <TableColumn>ACTION</TableColumn>
      </TableHeader>
      {loading ? (
  <TableBody isLoading={loading} loadingContent={<Spinner label="Loading..." />} />
) : (
  FinanceData && FinanceData.length > 0 ? (
    <TableBody isLoading={loading}>
      {FinanceData.map((value, key) => (
        <TableRow key={key}>
          <TableCell>{value.filename}</TableCell>
          <TableCell>{value.financial_year}</TableCell>
          <TableCell>
            <Actions data={value} setFinanceData={setFinanceData} FinanceData={FinanceData} />
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  ) : (
    <TableBody emptyContent={"No rows to display."} />
  )
)}


    </Table>
  );
};

export default TableView;
