import React, { useEffect, useState } from 'react'
import FaceRecog from "./FaceRecog";
const url = "http://127.0.0.1:8000";

function Home() {
    const [FaceDetected,setFaceDetected] = useState([]);
    useEffect(() => {
      const interval = setInterval(
        () => {
          fetch(url+"/userdata")
                .then((response) => {
                 //  console.log(response.json());
                  return response.json();
                 })
                 .then((data)=>{
                   setFaceDetected(data);
                   // console.log(data);
                 })}
        , 3000);
      return () => {
        clearInterval(interval);
      };
    }, []);
    return (
        <div className="front">
        <div > 
          <img className="App__camera" src={url+"/video"}></img>
        </div>
        <div className="App__container">
          <div className="App__list">
            {
              FaceDetected.map((item,i)=> 
              <FaceRecog key={i} name={item.user_name} address={item.user_address} path={url+item.user_image} phone={item.user_phone} email={item.user_email} uid={item.user_id} index={i}/>
              )}
              </div>
          </div>
        </div>

      
    )
}

export default Home
