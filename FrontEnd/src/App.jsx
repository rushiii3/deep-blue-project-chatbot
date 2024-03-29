import React, { Suspense, useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { LandingPage, Login, UploadPage, AddPdfPage } from "./Routes";
import NavbarShow from "./Component/Layout/Navbarshow";
import Navbars from "./Component/Layout/Navbar";
import Footer from "./Component/Layout/Footer";
import Loading from "./Component/Loader/Loading";
import { Toaster } from "react-hot-toast";
import { useUserStore, useDarkModeStore, useLoader } from "./Store/Store";
import axios from "axios";

export default function App() {
  const { loadUser } = useUserStore();
  const { mode, setMode } = useDarkModeStore();
  const { loading, setLoading } = useLoader();
  useEffect(() => {
    // Set up request interceptor
    const requestInterceptor = axios.interceptors.request.use(
      function (config) {
        // Do something before request is sent
        if (config.method.toUpperCase() === 'GET') {
          setLoading(true);
        }
        return config;
      },
      function (error) {
        // Do something with request error
        setLoading(false);
        return Promise.reject(error);
      }
    );
  
    // Set up response interceptor
    const responseInterceptor = axios.interceptors.response.use(
      function (response) {
        // Do something with response data
        setLoading(false);
        return response;
      },
      function (error) {
        // Do something with response error
        setLoading(false);
        return Promise.reject(error);
      }
    );
  
    // Clean up interceptors on component unmount
    return () => {
      axios.interceptors.request.eject(requestInterceptor);
      axios.interceptors.response.eject(responseInterceptor);
    };
  }, []); // Run only once on component mount
  

  useEffect(() => {
    // Function to check the preferred color scheme
    const checkColorScheme = () => {
      setMode(window.matchMedia("(prefers-color-scheme: dark)").matches);
    };

    // Call checkColorScheme on component mount to initialize the state
    checkColorScheme();

    // Add listener for changes in preferred color scheme
    const mediaQueryList = window.matchMedia("(prefers-color-scheme: dark)");
    const handleChange = (event) => {
      setMode(event.matches);
    };
    mediaQueryList.addEventListener("change", handleChange);

    // Clean up listener on component unmount
    return () => {
      mediaQueryList.removeEventListener("change", handleChange);
    };
  }, []);
  useEffect(() => {
    loadUser();
  }, []);

  return (
    <main className={`${mode ? "dark text-foreground bg-background" : ""}`}>
      <Toaster />
      <Router>
        <NavbarShow>
          <Navbars />
        </NavbarShow>

        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/add" element={<AddPdfPage />} />
          </Routes>
        </Suspense>
      </Router>
    </main>
  );
}
