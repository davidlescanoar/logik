import React, {Component} from 'react';
import LoginButton from "../LoginButton/LoginButton";
import LogoutButton from "../LogoutButton/LogoutButton";
import {useAuth0} from "@auth0/auth0-react";

export default function Home() {
    const { user } = useAuth0();
    return (
        <div>
            Home
            {JSON.stringify(user, null, 2)}
        </div>
    );
}