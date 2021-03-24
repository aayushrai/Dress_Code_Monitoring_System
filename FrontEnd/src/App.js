import React, { useEffect, useState } from 'react';
import Header from './Header';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from './Home'
import Checkout from './Checkout';
import ProductSelect from './ProductSelect';
import Enroll from './Enroll';
const url = "http://127.0.0.1:8000";


function App() {


useEffect(() => {
  const interval = setInterval(
    () => {
      fetch(url+"/applydiscount")
            .then((response) => {
             //  console.log(response.json());
              return response.json();
             })
             .then((data)=>{
               // console.log(data);
             })}
    , 60000);
  return () => {
    clearInterval(interval);
  };
}, []);


      return (
        <Router>
        <div className="App">
          
          <Switch>
              <Route path="/checkout/:order_id/:total">
                <Header />
                <Checkout />
              </Route>
              <Route path="/productselect/:uid">
                <Header />
                <ProductSelect />
              </Route>
              <Route path="/enroll">
                <Header />
                <Enroll />
              </Route>
              <Route path="/">
                <Header />
                <Home />
              </Route>
            </Switch>
          </div>
          
      </Router>
      );
    }
    
    export default App;
    