#!/usr/bin/env python3
"""
Simple test client for the Scopa GameServer.
Tests the JSON protocol without needing the full Panda3D frontend.
"""

import socket
import json
import time


def send_command(sock, command):
    """Send a command and receive response."""
    print(f"\n>>> {command}")
    sock.sendall((command + "\n").encode("utf-8"))
    response = sock.makefile("r").readline()
    data = json.loads(response)
    print(f"<<< {json.dumps(data, indent=2)}")
    return data


def test_game_flow():
    """Test a complete game flow."""
    print("=" * 60)
    print("Scopa GameServer Test Client")
    print("=" * 60)

    try:
        # Connect
        print("\n1. Connecting to server...")
        sock = socket.create_connection(("127.0.0.1", 5000), timeout=5)
        print("✓ Connected")

        # Test HELLO
        print("\n2. Testing HELLO command...")
        response = send_command(sock, "HELLO")
        assert response["status"] == "ok"
        print("✓ HELLO command works")

        # Start game
        print("\n3. Starting new game...")
        response = send_command(sock, "START")
        assert response["status"] == "ok"
        assert "table" in response
        assert "player1" in response
        assert "player2" in response
        print(f"✓ Game started")
        print(f"  - Table: {len(response['table'])} cards")
        print(f"  - P1 hand: {len(response['player1']['hand'])} cards")
        print(f"  - P2 hand: {len(response['player2']['hand'])} cards")

        # Get game state
        print("\n4. Getting game state...")
        response = send_command(sock, "STATE")
        assert response["status"] == "ok"
        print("✓ STATE command works")

        # Try to get captures for first card
        print("\n5. Getting possible captures for first card...")
        response = send_command(sock, "CAPTURES 0")
        assert response["status"] == "ok"
        print(f"✓ Found {len(response['captures'])} possible capture(s)")

        # Play a card
        print("\n6. Playing first card...")
        capture_idx = 0 if len(response["captures"]) > 0 else -1
        response = send_command(sock, f"PLAY 0 {capture_idx}")
        assert response["status"] == "ok"
        print(f"✓ Card played successfully")
        print(f"  - Current player: {response['currentPlayer']}")
        print(f"  - Table now has: {len(response['table'])} cards")

        # Play a few more cards to test the flow
        print("\n7. Playing more cards...")
        for i in range(5):
            # Get state
            response = send_command(sock, "STATE")
            if response["roundOver"]:
                print("✓ Round is over!")
                break

            current_player = response["currentPlayer"]
            hand_size = (
                len(response["player1"]["hand"])
                if "Player 1" in current_player
                else len(response["player2"]["hand"])
            )

            if hand_size == 0:
                print("  - Current player has no cards")
                continue

            # Get captures
            response = send_command(sock, "CAPTURES 0")
            capture_idx = 0 if len(response["captures"]) > 0 else -1

            # Play card
            response = send_command(sock, f"PLAY 0 {capture_idx}")
            print(f"  - {current_player} played a card")

            time.sleep(0.1)

        # Finalize if needed
        print("\n8. Checking if round needs finalization...")
        response = send_command(sock, "STATE")
        if response["roundOver"]:
            print("  - Finalizing round...")
            response = send_command(sock, "FINALIZE")
            assert response["status"] == "ok"
            print("✓ Round finalized")

        # Get score
        print("\n9. Getting final score...")
        response = send_command(sock, "SCORE")
        assert response["status"] == "ok"
        print(f"✓ Score calculated:")
        print(f"  - Player 1: {response['player1Score']} points")
        print(f"  - Player 2: {response['player2Score']} points")

        # Quit
        print("\n10. Disconnecting...")
        response = send_command(sock, "QUIT")
        sock.close()
        print("✓ Disconnected")

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)

    except ConnectionRefusedError:
        print("\n❌ ERROR: Could not connect to server on port 5000")
        print("   Make sure the GameServer is running:")
        print("   cd scopa && ./run_server.sh")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_game_flow()
