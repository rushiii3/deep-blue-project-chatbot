import { useState } from "react";
import "./App.css";

import Footer from "./Component/Layout/Footer";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import {LandingPage,Login,UploadPage} from './Routes';
import NavbarShow from "./Component/Layout/Navbarshow";
import Navbar from "./Component/Layout/Navbar";
export default function App() {
  return (
    <div class="overflow-x-hidden antialiased">
      <Router>
        <NavbarShow>
        <Navbar />
        </NavbarShow>
    
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/upload" element={<UploadPage />} />

        
      </Routes>
      <NavbarShow>
      <Footer />

      </NavbarShow>
      </Router>
     
    </div>
  );
}
