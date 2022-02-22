import React, {useContext} from "react";

import {Request} from "../../utils/utils";
import {UserID, UserName} from "../CodeWars/CodeWarsClient";


export default function Dailies() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)

    const url = "http://127.0.0.1:8000/Habitica/Dailies/" + userID
    const data = Request(url, false)

    let due_dailies = <></>
    
    if(data) {

        const not_done = data.filter(daily => daily.isDue && !daily.completed)

        due_dailies = not_done.map((daily) => (
            <tr className={daily.priority === 1 ? "todoEntryTRP1" : "todoEntryTR"}>
                <td>
                    ▷ {daily.id}
                </td>
                <td className={"todoEntryTD"}>
                    {daily.priority}
                </td>
                <td className={"todoEntryTD"}>
                    {daily.text}
                </td>
            </tr>
        ))
    }

    return (
        <>
            <div className={"todoHeader"}>
                Dailies
            </div>
            <table>
                {due_dailies}
            </table>
        </>
    )
}