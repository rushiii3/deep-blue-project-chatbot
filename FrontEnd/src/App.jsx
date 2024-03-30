import React, { Suspense, useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { LandingPage, Login, UploadPage, AddPdfPage } from "./Routes";
import NavbarShow from "./Component/Layout/Navbarshow";
import Navbars from "./Component/Layout/Navbar";
import Footer from "./Component/Layout/Footer";
import Loading from "./Component/Loader/Loading";
import { Toaster } from "react-hot-toast";
import { useUserStore, useDarkModeStore } from "./Store/Store";
import Protected from "./Component/Protection/Protected";

export default function App() {
  const { loadUser } = useUserStore();
  const { mode, setMode } = useDarkModeStore();
  useEffect(() => {
    loadUser();
  }, []);

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
            <Route
              path="/add"
              element={
                <Protected>
                  <AddPdfPage />
                </Protected>
              }
            />
          </Routes>
        </Suspense>
      </Router>
    </main>
  );
}
