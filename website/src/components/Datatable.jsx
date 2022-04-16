import React from "react";
import DataTable from "react-data-table-component";
import styled from 'styled-components';
import Button from "./shared/Button";

const TextField = styled.input`
	height: 32px;
	width: 200px;
	border-radius: 3px;
	border-top-left-radius: 5px;
	border-bottom-left-radius: 5px;
	border-top-right-radius: 0;
	border-bottom-right-radius: 0;
	border: 1px solid #e5e5e5;
	padding: 0 32px 0 16px;
	&:hover {
		cursor: pointer;
	}
`;

const ClearButton = styled(Button)`
	border-top-left-radius: 0;
	border-bottom-left-radius: 0;
	border-top-right-radius: 5px;
	border-bottom-right-radius: 5px;
	height: 34px;
	width: 32px;
	text-align: center;
	display: flex;
	align-items: center;
	justify-content: center;
`;


const FilterComponent = ({ filterText, onFilter, onClear }) => (
    <>
        <TextField
            id="search"
            type="text"
            placeholder="Filter By Name"
            aria-label="Search Input"
            value={filterText}
            onChange={onFilter}
        />
        <ClearButton type="button" onClick={onClear}>
            X
        </ClearButton>
    </>
);
export default function ExampleTable({ columns = [
    {
        name: 'Title',
        selector: row => row.name,
    },
    {
        name: 'Year',
        selector: row => row.year,
    },
], data = [
    {
        id: 1,
        name: 'Beetlejuice',
        year: '1988',
    },
    {
        id: 2,
        name: 'Ghostbusters',
        year: '1984',
    },
] }) {
    const [filterText, setFilterText] = React.useState('Beetlejuice');
	const [resetPaginationToggle, setResetPaginationToggle] = React.useState(false);
	const filteredItems = data.filter(
		item => item.name && item.name.toLowerCase().includes(filterText.toLowerCase()),
	);

	const subHeaderComponentMemo = React.useMemo(() => {
		const handleClear = () => {
			if (filterText) {
				setResetPaginationToggle(!resetPaginationToggle);
				setFilterText('');
			}
		};

		return (
			<FilterComponent onFilter={e => setFilterText(e.target.value)} onClear={handleClear} filterText={filterText} />
		);
	}, [filterText, resetPaginationToggle]);
  return (
      <>    
    <DataTable
        title="Contact List"
        columns={columns}
        data={filteredItems}
        pagination
			paginationResetDefaultPage={resetPaginationToggle} // optionally, a hook to reset pagination to page 1
			subHeader
            subHeaderComponent={subHeaderComponentMemo}
			selectableRows
			persistTableHead
    />
    </>
  );
}
