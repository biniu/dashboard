import React, {useContext} from "react";

import {Request} from "../../utils/utils";
import {UserID, UserName} from "../CodeWars/CodeWarsClient";


export default function Habits() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)

    const url = "http://127.0.0.1:8000/Habitica/Habits/" + userID
    const data = Request(url, false)

    let habits = <></>

    console.log(data)

    if(data) {

        habits = data.map((habit) => (
            <tr className={habit.priority === 1 ? "todoEntryTRP1" : "todoEntryTR"}>
                <td>
                    ▷ {habit.id}
                </td>
                <td className={"todoEntryTD"}>
                    {habit.priority}
                </td>
                <td className={"todoEntryTD"}>
                    {habit.text}
                </td>
                <td className={"todoEntryTD"}>
                    UP {habit.counterUp}
                </td>
                <td className={"todoEntryTD"}>
                    DOWN {habit.counterDown}
                </td>
            </tr>
        ))
    }

    return (
        <>
            <div className={"todoHeader"}>
                Habits
            </div>
            <table>
                {habits}
            </table>
        </>
    )
}