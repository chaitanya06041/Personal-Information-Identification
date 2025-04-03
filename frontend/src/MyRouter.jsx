import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
function MyRouter() {
  return (
    <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<Home />}></Route>
            <Route path="/history" element={<></>}></Route>
        </Routes>
    </Router>
  )
}

export default MyRouter
