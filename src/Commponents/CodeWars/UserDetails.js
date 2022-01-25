import React, {useContext} from "react";

import {UserName} from "./CodeWarsClient";

import {Request} from "../../utils/utils";

import './CodeWars.css'


export default function UserDetails() {
    const userName = useContext(UserName)
    const url = "http://127.0.0.1:8000/code_wars/UserStatistics/"

    const data = Request(url, false)

    const position = (last, penultimate) => {
        if (last['leaderboardPosition'] === penultimate['leaderboardPosition']) {
            return last['leaderboardPosition'] + " No Changes"
        } else if (last['leaderboardPosition'] < penultimate['leaderboardPosition']) {
            return last['leaderboardPosition'] + " Up"
        } else {
            return last['leaderboardPosition'] + " Down"
        }
    }

    const out = () => {
        if (data) {
            const last = data['results'].find((score, index) => {
                if (score.id === data.count)
                    return true;
            })
            const penultimate = data['results'].find((score, index) => {
                if (score.id === data.count - 1)
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
