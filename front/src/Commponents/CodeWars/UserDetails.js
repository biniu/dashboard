import React, {useContext} from "react";

import {UserID, UserName} from "./CodeWarsClient";

import {getTodayDate, getYesterdayDate, Request} from "../../utils/utils";

import './CodeWars.css'


export default function UserDetails() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)
    const url = "http://127.0.0.1:8000/CodeWars/UserStatistics/" + userID

    const data = Request(url, false)

    const position = (last, penultimate) => {
        if (last['leaderboard_position'] === penultimate['leaderboard_position']) {
            return last['leaderboard_position'] + " No Changes"
        } else if (last['leaderboard_position'] < penultimate['leaderboard_position']) {
            return last['leaderboard_position'] + " Up"
        } else {
            return last['leaderboard_position'] + " Down"
        }
    }

    const out = () => {
        if (data) {
            console.log(data)
            const last = data.find((score, index) => {
                if (score.last_update === getTodayDate())
                    return true;
            })

            console.log(last)

            const penultimate = data.find((score, index) => {
                if (score.last_update === getYesterdayDate())
                    return true;
            })

            return (
                <table className={"codeWarsTable"}>
                    <tr>
                        <td className={"cwTD"}> -> User name:</td>
                        <td className={"cwTD"}>{userName}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Honor:</td>
                        <td className={"cwTD"}>{last['honor']}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Position:</td>
                        <td className={"cwTD"}>{position(last, penultimate)}</td>
                    </tr>
                    <tr>
                        <td className={"cwTD"}> -> Completed kata:</td>
                        <td className={"cwTD"}>{last['kata_completed']}</td>
                    </tr>

                </table>
            )
        } else {
            return "Loading data ..."
        }
    }

    return (out());
}
