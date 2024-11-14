#!/usr/bin/env python
# coding: utf-8

# In[2]:


from qiskit.circuit import CircuitInstruction
from qiskit import QuantumCircuit, Aer, transpile
import warnings

warnings.filterwarnings('ignore') # Check some issues

class CircuitErrorFiltering:
    def __init__(self, 
                 quantum_circuit: QuantumCircuit, 
                 EF_qreg: int,
                 basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
                ) -> None:
        
        self.quantum_circuit = quantum_circuit
        self.EF_qreg = EF_qreg
        self.basis_gates = basis_gates
        self.encode_qreg = self.quantum_circuit.num_qubits
        self.auxi_qreg = self.quantum_circuit.num_qubits + 1
    
    """ Check variable 'quantum_circuit' """
    @property
    def quantum_circuit(self) -> QuantumCircuit:
        return self.__quantum_circuit
    
    @quantum_circuit.setter
    def quantum_circuit(self, 
                        quantum_circuit: QuantumCircuit
                       ) -> None:
        
        if type(quantum_circuit) == QuantumCircuit:
            self.__quantum_circuit = quantum_circuit
        else:
            raise ValueError('Invalue variable type: quantum_circuit')
    
    
    """ Check variable 'EF_qreg' """
    @property
    def EF_qreg(self) -> int:
        return self.__EF_qreg
    
    @EF_qreg.setter
    def EF_qreg(self, 
                EF_qreg: int
               ) -> None:
        
        # EF_qreg가 초기 회로 큐비트 개수 사이에 있도록 설정
        if type(EF_qreg) == int:
            if EF_qreg >=0 and EF_qreg < self.quantum_circuit.num_qubits:
                self.__EF_qreg = EF_qreg
            else:
                raise ValueError('Invalue variable: EF_qreg (It must be between {} to {})'
                                .format(0, self.quantum_circuit.num_qubits-1))
        else:
            raise ValueError('Invalue variable type: EF_qreg')
    
    """ Check variable 'basis_gates' """
    @property
    def basis_gates(self) -> list:
        return self.__basis_gates
    
    @basis_gates.setter
    def basis_gates(self, 
                    basis_gates: list
                   ) -> None:
        
        if type(basis_gates) == list:
            self.__basis_gates = basis_gates
        else:
            raise ValueError('Invalue variable type: basis_gates')
    
    
    """ Reconstruct quantum circuit with error filtering """
    def SingleQubitBitFlip(self) -> QuantumCircuit:
        
        # Get transpiled quantum circuit
        quantum_circuit_transpiled = transpile(circuits = self.quantum_circuit, 
                                               basis_gates = self.basis_gates)
        
        def ConvertToLogicalGate(circuit_data: CircuitInstruction, 
                                 qc: QuantumCircuit
                                ) -> None:
            # Check single gate
            if len(circuit_data.qubits) == 1:
                if circuit_data.qubits[0].index == self.EF_qreg: # Convert to logical gate
                    if circuit_data.operation.name == 'id':
                        qc.id(circuit_data.qubits[0].index)
                        qc.id(self.encode_qreg)
                    elif circuit_data.operation.name == 'rz':
                        qc.rz(circuit_data.operation.params[0], circuit_data.qubits[0].index)
                        qc.id(self.encode_qreg)
                    elif circuit_data.operation.name == 'sx':
                        qc.cx(circuit_data.qubits[0].index, self.encode_qreg)
                        qc.sx(circuit_data.qubits[0].index)
                        qc.cx(circuit_data.qubits[0].index, self.encode_qreg)
                    elif circuit_data.operation.name == 'x':
                        qc.x(circuit_data.qubits[0].index)
                        qc.x(self.encode_qreg)
                    else:
                        raise ValueError('Undifined basis gate set')
                else: # Do nothing
                    if circuit_data.operation.name == 'id':
                        qc.id(circuit_data.qubits[0].index)
                    elif circuit_data.operation.name == 'rz':
                        qc.rz(circuit_data.operation.params[0], circuit_data.qubits[0].index)
                    elif circuit_data.operation.name == 'sx':
                        qc.sx(circuit_data.qubits[0].index)
                    elif circuit_data.operation.name == 'x':
                        qc.x(circuit_data.qubits[0].index)
                    else:
                        raise ValueError('Undifined basis gate set')
            # Check two-qubit gate
            elif len(circuit_data.qubits) == 2:
                if circuit_data.qubits[0].index == self.EF_qreg: # If control part is targeted
                    if circuit_data.operation.name == 'cx':
                        qc.cx(circuit_data.qubits[0].index, circuit_data.qubits[1].index)
                    else:
                        raise ValueError('Undifined basis gate set')
                elif circuit_data.qubits[1].index == self.EF_qreg: # If target part is targeted
                    if circuit_data.operation.name == 'cx':
                        qc.cx(circuit_data.qubits[0].index, circuit_data.qubits[1].index)
                        qc.cx(circuit_data.qubits[0].index, self.encode_qreg)
                    else:
                        raise ValueError('Undifined basis gate set')
                else: # Do nothing
                    if circuit_data.operation.name == 'cx':
                        qc.cx(circuit_data.qubits[0].index, circuit_data.qubits[1].index)
                    else:
                        raise ValueError('Undifined basis gate set')
            # Check invalid gate
            else:
                raise ValueError('Invalue circuit instruction (check the barrier or measurements)')
        
        # Rebuild quantum circuit with additional qubits (encoding, auxi)
        qc = QuantumCircuit(self.quantum_circuit.num_qubits + 2)    
        
        # Encoding
        qc.cx(self.EF_qreg, self.encode_qreg)
    
        # Convert quantum gates to logical
        for i in range(len(quantum_circuit_transpiled.data)):
            ConvertToLogicalGate(quantum_circuit_transpiled.data[i], qc)
            #qc.barrier()
            
        
        
        # Parity check
        qc.cx(self.EF_qreg, self.auxi_qreg)
        qc.cx(self.encode_qreg, self.auxi_qreg)
        
        # Decoding
        qc.cx(self.EF_qreg, self.encode_qreg)
        
        # Measurement
        qc.measure_all()
        
        return qc        
    
    #################### Work in progress
    def SingleQubitPhaseFlip(self):
        pass
    
    #################### Work in progress
    def SingleQubitErrorFiltering(self):
        pass
    
    """ Probability distribution post-processing """
    def PostProcessing(self) -> None:
        __shots = 1000
        __num_qubits = self.quantum_circuit.num_qubits + 2
        __backend_sim = Aer.get_backend('qasm_simulator')
        __job_sim = __backend_sim.run(self.SingleQubitBitFlip(), shots=__shots)
        __counts = __job_sim.result().get_counts()
        
        # Parameter setting
        __counts_postprocess = {}

        # bitstrings
        __format_bitstring = '{0:0' + str(self.quantum_circuit.num_qubits) + 'b}'
        __bitstring_keys = [__format_bitstring.format(ii) for ii in range(2**self.quantum_circuit.num_qubits)]
        __counts_postprocess = {key: 0 for key, value in dict.fromkeys(__bitstring_keys).items()}
        
        for result_string in __counts:
            if result_string[0:2] == '00':
                __counts_postprocess[result_string[2:__num_qubits]] = __counts[result_string]
        
        print('Probability of post-selection:', sum(__counts_postprocess.values())/__shots)
        print('Post processed counts:', __counts_postprocess)
        
        return __counts_postprocess


# In[ ]:




