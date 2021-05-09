import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Table as BasicTable} from '@material-ui/core';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles({
    table: {
        minWidth: 650,
    },
});

function createData(url, points, ac) {
    return [url, points, ac];
}

const cols = ['URL', 'Puntaje', 'AC'];

const rows = [
    createData('Frozen yoghurt', 159, 6.0),
    createData('Ice cream sandwich', 237, 9.0),
    createData('Eclair', 262, 16.0),
    createData('Cupcake', 305, 3.7),
    createData('Gingerbread', 356, 16.0),
];

export default function Table() {
    const classes = useStyles();

    return (
        <TableContainer component={Paper}>
            <BasicTable className={classes.table} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        {cols.map((col, index) => {
                            return (
                                <TableCell align={index ? "right" : "left"}>
                                    {col}
                                </TableCell>
                            );
                        })}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map(row => {
                        return (
                            <TableRow key={row}>
                                {row.map((col, index) => {
                                    return (
                                        <TableCell component="th" scope="row" align={index ? "right" : "left"}>
                                            {col}
                                        </TableCell>
                                    );
                                })}
                            </TableRow>
                        );
                    })}
                </TableBody>
            </BasicTable>
        </TableContainer>
    );
}