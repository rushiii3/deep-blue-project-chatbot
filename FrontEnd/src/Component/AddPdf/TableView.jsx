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
  const { FinanceData, setFinanceData } = useFinanceStore();
  const [selectedKeys, setSelectedKeys] = React.useState(new Set([]));
  
  useEffect(() => {


    
    const getData = async () => {
      setLoading(true);
      try {
        const { data } = await axios.get(`${link}/get-data`);
        if (data.success) {
          setFinanceData(data.data);
          if (data.data) {
            console.log(data.data);
            const selected = data.data
              .filter((value) => value?.isSelected)
              .map((value) => value?._id);
            const updatedSelectedKeys = new Set(selected);
            setSelectedKeys(updatedSelectedKeys);

          }
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, []);
  const handleSelection = async(e) => {
    console.log(e);
    const myArray = Array.from(e); // Convert Set to array
    const myValue = myArray[0];
    const filteredData = FinanceData.filter(item => item._id === myValue);
    const filteredUrls = filteredData.map(item => item.pdf.url);
    console.log(filteredUrls[0]);
    try {
      const {data} = await axios.post("https://fantastic-eureka-6x6jg4r94p73475-5000.app.github.dev/api/extraction",{url:myValue,id:filteredUrls[0]})
      console.log(data);
    } catch (error) {
      
    }
    setSelectedKeys(e)
  }
  return (
    <Table
      aria-label="Example static collection table"
      classNames={{
        wrapper: "max-h-[382px]",
      }}
      selectionMode="single"
      color="primary"
      defaultSelectedKeys={selectedKeys}
      onSelectionChange={handleSelection}
      selectedKeys={selectedKeys}
    >
      <TableHeader>
        <TableColumn>NAME</TableColumn>
        <TableColumn>YEAR</TableColumn>
        <TableColumn>ACTION</TableColumn>
      </TableHeader>
      {loading ? (
        <TableBody
          isLoading={loading}
          loadingContent={<Spinner label="Loading..." />}
        />
      ) : FinanceData && FinanceData.length > 0 ? (
        <TableBody isLoading={loading}>
          {FinanceData.map((value, key) => (
            <TableRow key={value?._id}>
              <TableCell>{value.filename.slice(0, -4)}</TableCell>
              <TableCell>{value.financial_year}</TableCell>
              <TableCell>
                <Actions
                  data={value}
                  setFinanceData={setFinanceData}
                  FinanceData={FinanceData}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      ) : (
        <TableBody emptyContent={"No rows to display."} />
      )}
    </Table>
  );
};

export default TableView;
