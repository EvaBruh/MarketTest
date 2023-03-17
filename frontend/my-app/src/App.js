import React from "react";
import { Route, Routes } from "react-router-dom";

import AUDD from "./components/AUDD";

import './App.css';

const App = () => {

  return (
    <Routes>
        <Route index element={<AUDD />} />
    </Routes>
  )
}

export default App;