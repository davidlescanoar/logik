import React, {Component} from 'react';
import Table from "../Table/Table";
import Typography from '@material-ui/core/Typography';

export default function Problems() {
    return (
        <div>
            <Typography variant="h5" gutterBottom>
                Problemas
            </Typography>
            <Table/>
        </div>
    );
}