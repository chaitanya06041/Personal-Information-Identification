import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import Navbar from "./components/Navbar";
import Home from "./components/Home";
import LaunchPage from "./components/LaunchPage";
function MyRouter() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<LaunchPage />}></Route>
            <Route path="/mask" element={<Home />}></Route>
        </Routes>
    </Router>
  )
}

export default MyRouter
