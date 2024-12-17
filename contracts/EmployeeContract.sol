// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmployeeContract {
    struct Employee {
        uint256 empID;
        string firstName;
        string lastName;
        string jobTitle;
        uint256 performanceScore;
    }

    mapping(address => Employee) private employees;
    mapping(address => bool) private employeeExists;

    // Events for debugging and tracking
    event DebugMessage(string message);
    event EmployeeAdded(address indexed employeeAddress, uint256 empID, string firstName, string lastName);
    event EmployeeUpdated(address indexed employeeAddress, string firstName, string lastName, string jobTitle, uint256 performanceScore);

    // Modifier: Check if employee does not exist
    modifier employeeDoesNotExist(address _employeeAddress) {
        require(!employeeExists[_employeeAddress], "Employee already exists");
        _;
    }

    // Modifier: Check if employee exists
    modifier employeeExistsCheck(address _employeeAddress) {
        require(employeeExists[_employeeAddress], "Employee does not exist");
        _;
    }

    // Add a new employee (Anyone can call this function)
    function addEmployee(
        address _employeeAddress,
        uint256 _empID,
        string memory _firstName,
        string memory _lastName,
        string memory _jobTitle,
        uint256 _performanceScore
    ) public employeeDoesNotExist(_employeeAddress) {
        require(_employeeAddress != address(0), "Employee address cannot be zero address");
        require(_empID > 0, "Employee ID must be greater than 0");
        require(bytes(_firstName).length > 0, "First name cannot be empty");
        require(bytes(_lastName).length > 0, "Last name cannot be empty");
        require(bytes(_jobTitle).length > 0, "Job title cannot be empty");

        employees[_employeeAddress] = Employee(_empID, _firstName, _lastName, _jobTitle, _performanceScore);
        employeeExists[_employeeAddress] = true;

        emit EmployeeAdded(_employeeAddress, _empID, _firstName, _lastName);
    }

    // Get employee data by address (View-only function)
    function getEmployee(address _employeeAddress)
        public
        view
        employeeExistsCheck(_employeeAddress)
        returns (uint256 empID, string memory firstName, string memory lastName, string memory jobTitle, uint256 performanceScore)
    {
        Employee memory employee = employees[_employeeAddress];
        return (employee.empID, employee.firstName, employee.lastName, employee.jobTitle, employee.performanceScore);
    }

    // Update existing employee data (Anyone can call this function)
event DebugMessage(string message, address employeeAddress);

function updateEmployee(
    address _employeeAddress,
    string memory _firstName,
    string memory _lastName,
    string memory _jobTitle,
    uint256 _performanceScore
) public employeeExistsCheck(_employeeAddress) {
    emit DebugMessage("Updating employee...", _employeeAddress);
    Employee storage employee = employees[_employeeAddress];
    employee.firstName = _firstName;
    employee.lastName = _lastName;
    employee.jobTitle = _jobTitle;
    employee.performanceScore = _performanceScore;

    emit DebugMessage("Employee updated successfully", _employeeAddress);
}

}
