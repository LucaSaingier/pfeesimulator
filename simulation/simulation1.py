import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from communication_infrastructure.infrastructure import CommunicationInfrastructure


def main():
    infra = CommunicationInfrastructure()
    print("Main thread started...")


if __name__ == "__main__":
    main()