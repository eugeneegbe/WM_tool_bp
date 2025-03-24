import React, {useState, useEffect} from 'react';
import './Home.scss';
import { Logger } from 'sass';

export default function Home() {
//   const [statusData, setStatusData] = useState()

//   useEffect(() => {
//     async function getStatusData() {
//       const res = await fetch(`http://127.0.0.1:5000/status`)
//       if(!res.ok){
//         const message = `Something went wrong: $(res.message)`
//         window.alert(message)
//       }
      
//       const statusData = await res.json();
//       setStatusData(statusData);
//       console.log(statusData);
//     }

//     getStatusData();
//     return;
//   },[]);

  return (
    <div>
        <h3> WD Tool Template </h3>
        {/* <p>{JSON.stringify(statusData)}</p> */}
    </div>
  );

}