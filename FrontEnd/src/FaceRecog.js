import React from 'react';
import "./FaceRecog.css";
import Button from '@material-ui/core/Button';
import {
  useHistory,Link
} from "react-router-dom";
const url = "http://127.0.0.1:8000";

function FaceRecog({name,address,path,phone,email,uid,index}) {
  const history = useHistory();
  const screenShot = ()=> {
    const requestOptions = {    
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"order_id":"image"})
        };
    fetch(url+'/screenshot', requestOptions)
    .then(response => response.json())
    .then(data => {
        history.push("/enroll");
    })}
  const unknownHandler = (index) => {
    if (index===0) {
      return(
        <div className="FaceRecog">
        <img className="FaceRecog__image" src={path}></img>
        <div className="FaceRecog__details">
          <div className="FaceRecog__text">
            <div className="FaceRecog__name"><span style={{color:"grey"}}>Name: </span>{name}</div>
            <div className="FaceRecog__address"><span style={{color:"grey"}}>Address: </span>{address}</div>
            <div className="FaceRecog__phone"><span style={{color:"grey"}}>Contact: </span>{phone}</div>
            <div className="FaceRecog__email"><span style={{color:"grey"}}>Email: </span>{email}</div>
          </div>
            <div className="FaceRecog__button">
              <Button variant="contained" color="primary" onClick={()=>{screenShot()}} >
                Add Unknown
              </Button>
            </div>
        </div>
    </div>
      ) ;
    }
    return(
    <div className="FaceRecog">
    <img className="FaceRecog__image" src={path}></img>
    <div className="FaceRecog__details">
      <div className="FaceRecog__text">
        <div className="FaceRecog__name"><span style={{color:"grey"}}>Name: </span>{name}</div>
        <div className="FaceRecog__address"><span style={{color:"grey"}}>Address: </span>{address}</div>
        <div className="FaceRecog__phone"><span style={{color:"grey"}}>Contact: </span>{phone}</div>
        <div className="FaceRecog__email"><span style={{color:"grey"}}>Email: </span>{email}</div>
      </div>
      <div className="FaceRecog__button">
        <Link to={"/productselect/"+uid}>
          <Button variant="contained" color="primary" >
            Verify Customer
          </Button>
        </Link>
      </div>
    </div> 
</div>
);
  };
    return (
     unknownHandler(index)
    )
}

export default FaceRecog
