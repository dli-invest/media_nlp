import React from "react";
import DataTable from "react-data-table-component";

const FilterComponent = ({ filterText, onFilter, onClear }) => (
    <>
        <input
            id="search"
            className="uk-input"
            type="text"
            placeholder="Filter By Name"
            aria-label="Search Input"
            value={filterText}
            onChange={onFilter}
        />
        <button type="button" className="uk-button uk-button-default" onClick={onClear}>
            X
        </button>
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
