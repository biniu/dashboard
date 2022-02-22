import React, {useContext} from "react";

import {Request} from "../../utils/utils";
import {UserID, UserName} from "../CodeWars/CodeWarsClient";


export default function Dailies() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)

    const url = "http://127.0.0.1:8000/Habitica/Dailies/" + userID
    const data = Request(url, false)

    let todos_not_done = <></>

    console.log(data)

    if(data) {

        const not_done = data.filter(todo => !todo.completed)

        todos_not_done = not_done.map((todo) => (
            <tr className={todo.priority === 1 ? "todoEntryTRP1" : "todoEntryTR"}>
                <td>
                    ▷ {todo.id}
                </td>
                <td className={"todoEntryTD"}>
                    {todo.priority}
                </td>
                <td className={"todoEntryTD"}>
                    {todo.text}
                </td>
            </tr>
        ))
    }

    return (
        <>
            <div className={"todoHeader"}>
                Dailys
            </div>
            <table>
                {todos_not_done}
            </table>
        </>
    )
}