
import "./App.css";
import React, { Suspense, lazy } from 'react';
import Footer from "./Component/Layout/Footer";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import { LandingPage, Login, UploadPage } from './Routes';
import NavbarShow from "./Component/Layout/Navbarshow";
import Navbar from "./Component/Layout/Navbar";
import Loading from "./Component/Loader/Loading";


export default function App() {
  return (
    <div class="overflow-x-hidden antialiased">
      <Router>
        <NavbarShow>
        <Navbar />
        </NavbarShow>
    
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/upload" element={<UploadPage />} />
          </Routes>
        </Suspense>
      <NavbarShow>
      <Footer />

      </NavbarShow>
      </Router>
     
    </div>
  );
}
