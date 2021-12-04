import React, {useContext} from "react";

import {UserName} from "./CodeWarsClient";

import {getTodayDate, getYesterdayDate, Request} from "../../utils/utils";

import './CodeWars.css'


export default function UserDetails() {
    const userName = useContext(UserName)
    const url = "http://127.0.0.1:8000/code_wars/UserStatistics/?last_update=" + getTodayDate()
    const urlYesterday = "http://127.0.0.1:8000/code_wars/UserStatistics/?last_update=" + getYesterdayDate()

    let data = Request(url)
    let dataYesterday = Request(urlYesterday)

    const position = () => {
        if (data[0]['leaderboardPosition'] === dataYesterday[0]['leaderboardPosition']) {
            return data[0]['leaderboardPosition'] + " No Changes"
        } else if (data[0]['leaderboardPosition'] < dataYesterday[0]['leaderboardPosition']) {
            return data[0]['leaderboardPosition'] + " Up"
        } else {
            return data[0]['leaderboardPosition'] + " Down"
        }
    }

    const out = () => {
        if (data && dataYesterday) {
            return (
                <table className={"codeWarsTable"}>
                    <tr>
                        <td className={"cwTD"}> -> User name:</td>
                        <td className={"cwTD"}>{userName}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Honor:</td>
                        <td className={"cwTD"}>{data[0]['honor']}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Position:</td>
                        <td className={"cwTD"}>{position()}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Completed kata:</td>
                        <td className={"cwTD"}>{data[0]['kata_completed']}</td>
                    </tr>

                </table>
            )
        } else {
            return "Loading data ..."
        }
    }

    return (out());
}
