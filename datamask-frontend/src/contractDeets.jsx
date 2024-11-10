import { ethers } from 'ethers';
import VideoStorage from './artifacts/contracts/Upload.sol/VideoStorage.json';
import { Buffer } from 'buffer';

// Ensure Buffer is available globally
window.Buffer = Buffer;

let account = '';
let contractGlobal = null;

async function loadProvider() {
  // Ensure the provider is loaded only if Metamask is available
  if (window.ethereum) {
    try {
      const newProvider = new ethers.providers.Web3Provider(window.ethereum);
      
      // Request wallet connection and get account details
      await newProvider.send('eth_requestAccounts', []);
      const signer = newProvider.getSigner();
      account = await signer.getAddress();
      console.log('Connected account:', account);
      
      // Load contract
      const contractAddress = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512';
      const newContract = new ethers.Contract(contractAddress, VideoStorage.abi, signer);
      contractGlobal = newContract;
      
      console.log('Contract:', newContract);
      return newContract;
    } catch (error) {
      console.error('Error connecting to MetaMask:', error);
      throw error;
    }
  } else {
    console.error('Ethereum object not found, install MetaMask.');
    throw new Error('MetaMask not installed');
  }
}

// uploading video to the blockchain
const uploadVideo = async (file, result) => {
  try {
    // Ensure provider and contract are loaded
    if (!contractGlobal) {
      await loadProvider();
    }
    
    if (!file) {
      throw new Error('No file provided');
    }
    
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const videoHash = ethers.utils.keccak256(buffer);
    
    // Call the contract function
    const tx = await contractGlobal.addVideo(videoHash, result);
    await tx.wait();
    
    console.log('Video uploaded successfully');
    return { success: true, message: 'Video uploaded successfully' };
  } catch (err) {
    console.error('Error uploading video:', err);
    throw err;
  }
};

// fetching the user's uploaded videos
const fetchVideos = async () => {
  try {
    // Ensure provider and contract are loaded
    if (!contractGlobal) {
      await loadProvider();
    }
    
    const videos = await contractGlobal.getUserVideos(account);
    
    if (videos.length === 0) {
      console.log('No videos found');
      return [];
    }
    
    console.log('Fetched videos:', videos);
    return videos;
  } catch (err) {
    console.error('Error fetching videos:', err);
    throw err;
  }
};

export { uploadVideo, fetchVideos, loadProvider };
