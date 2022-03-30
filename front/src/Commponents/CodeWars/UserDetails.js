import React, {useContext} from "react";

import {UserID, UserName} from "./CodeWarsClient";

import {Request} from "../../utils/utils";

import './CodeWars.css'


export default function UserDetails() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)
    const url = "/api/CodeWars/UserStatistics/" + userID

    const data = Request(url, false)

    const position = (last, penultimate) => {
        try {
            if (last['leaderboard_position'] === penultimate['leaderboard_position']) {
                return last['leaderboard_position'] + " No Changes"
            } else if (last['leaderboard_position'] < penultimate['leaderboard_position']) {
                return last['leaderboard_position'] + " Up"
            } else {
                return last['leaderboard_position'] + " Down"
            }
        } catch (TypeError) {
            return "No Data"
        }
    }

    const out = () => {
        if (data) {

            const sorted_data = data.sort((a, b) => {
                let da = new Date(a.last_update),
                    db = new Date(b.last_update);
                return da - db;
            })

            const last = sorted_data[sorted_data.length - 1]
            const penultimate = sorted_data[sorted_data.length - 2]

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
