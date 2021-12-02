import React, {useCallback, useState} from "react";
import axios from "axios";

import './CodeWars.css'


export default function UserDetails() {
    let [userData, setUserData] = useState('');
    const fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": "http://localhost:3001/codeWarsUser",
        })
            .then((response) => {
                setUserData(response.data)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])
    React.useEffect(() => {
        fetchData()
    }, [fetchData])


    return (
        <table className={"codeWarsTable"}>
            <tr>
                <td className={"cwTD"}> -> User name:</td>
                <td className={"cwTD"}>{userData['username']}</td>
            </tr>
            <tr>
                <td className={"cwTD"}> -> Honor:</td>
                <td className={"cwTD"}>{userData['honor']}</td>
            </tr>
            <tr>
                <td className={"cwTD"}> -> Position:</td>
                <td className={"cwTD"}>{userData['leaderboardPosition']}</td>
            </tr>
        </table>
    );
}
