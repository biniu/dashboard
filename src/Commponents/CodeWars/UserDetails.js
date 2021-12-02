import React, {useCallback, useState} from "react";
import axios from "axios";

import './CodeWars.css'


export default function UserDetails() {
    let [data, setData] = useState('');
    const fetchData = useCallback(() => {
        axios({
            "method": "GET",
            "url": "http://127.0.0.1:8000/code_wars/UserStatistics/",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
            .then((response) => {
                setData(response.data)
            })
            .catch((error) => {
                console.log(error)
            })
    }, [])
    React.useEffect(() => {
        fetchData()
    }, [fetchData])

    let userData = ""

    if (data['results']) {
        console.log(data['results'][0])
        userData = data['results'][0]
    }

    return (
        <table className={"codeWarsTable"}>
            <tr>
                <td className={"cwTD"}> -> User name:</td>
                <td className={"cwTD"}>Biniu</td>
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
