import React, {useContext} from "react";

import {Request} from "../../utils/utils";
import {UserID, UserName} from "../CodeWars/CodeWarsClient";


export default function Todos() {
    const userName = useContext(UserName)
    const userID = useContext(UserID)

    const url = "/api/Habitica/Todo/" + userID
    const data = Request(url, false)

    let todos_not_done = <></>

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
            Todos
        </div>
        <table>
            {todos_not_done}
        </table>
        </>
    )
}